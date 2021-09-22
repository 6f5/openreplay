from chalicelib.core import sessions_metas
from chalicelib.utils import args_transformer
from chalicelib.utils import helper, dev
from chalicelib.utils import pg_client
from chalicelib.utils.TimeUTC import TimeUTC
from chalicelib.utils.metrics_helper import __get_step_size
import math
from chalicelib.core.dashboard import __get_constraints, __get_constraint_values


def __transform_journey(rows):
    nodes = []
    links = []
    for r in rows:
        source = r["source_event"][r["source_event"].index("_"):]
        target = r["target_event"][r["target_event"].index("_"):]
        if source not in nodes:
            nodes.append(source)
        if target not in nodes:
            nodes.append(target)
        links.append({"source": nodes.index(source), "target": nodes.index(target), "value": r["value"]})
    return {"nodes": nodes, "links": sorted(links, key=lambda x: x["value"], reverse=True)}


JOURNEY_DEPTH = 5
JOURNEY_TYPES = {
    "PAGES": {"table": "events.pages", "column": "base_path", "table_id": "message_id"},
    "CLICK": {"table": "events.clicks", "column": "label", "table_id": "message_id"},
    "VIEW": {"table": "events_ios.views", "column": "name", "table_id": "seq_index"},
    "EVENT": {"table": "events_common.customs", "column": "name", "table_id": "seq_index"}
}


@dev.timed
def get_journey(project_id, startTimestamp=TimeUTC.now(delta_days=-1), endTimestamp=TimeUTC.now(), filters=[], **args):
    pg_sub_query_subset = __get_constraints(project_id=project_id, data=args, duration=True, main_table="sessions",
                                            time_constraint=True)
    event_start = None
    event_table = JOURNEY_TYPES["PAGES"]["table"]
    event_column = JOURNEY_TYPES["PAGES"]["column"]
    event_table_id = JOURNEY_TYPES["PAGES"]["table_id"]
    extra_values = {}
    for f in filters:
        if f["type"] == "START_POINT":
            event_start = f["value"]
        elif f["type"] == "EVENT_TYPE" and JOURNEY_TYPES.get(f["value"]):
            event_table = JOURNEY_TYPES[f["value"]]["table"]
            event_column = JOURNEY_TYPES[f["value"]]["column"]
        elif f["type"] in [sessions_metas.meta_type.USERID, sessions_metas.meta_type.USERID_IOS]:
            pg_sub_query_subset.append(f"sessions.user_id = %(user_id)s")
            extra_values["user_id"] = f["value"]

    with pg_client.PostgresClient() as cur:
        pg_query = f"""SELECT source_event,
                               target_event,
                               MAX(target_id)  max_target_id,
                               MAX(source_id) max_source_id,
                               count(*) AS      value
                        
                        FROM (SELECT event_number || '_' || value as target_event,
                                     message_id AS target_id,
                                     LAG(event_number || '_' || value, 1) OVER ( PARTITION BY session_rank ) AS source_event,
                                     LAG(message_id, 1) OVER ( PARTITION BY session_rank ) AS source_id
                              FROM (SELECT value,
                                           session_rank,
                                           message_id,
                                           ROW_NUMBER() OVER ( PARTITION BY session_rank ORDER BY timestamp ) AS event_number
                                    
                                    {f"FROM (SELECT * FROM (SELECT *, MIN(mark) OVER ( PARTITION BY session_id , session_rank ORDER BY timestamp ) AS max FROM (SELECT *, CASE WHEN value = %(event_start)s THEN timestamp ELSE NULL END as mark"
        if event_start else ""}
                                    
                                    FROM (SELECT session_id,
                                                 message_id,
                                                 timestamp,
                                                 value,
                                                 SUM(new_session) OVER (ORDER BY session_id, timestamp) AS session_rank
                                          FROM (SELECT *,
                                                       CASE
                                                           WHEN source_timestamp IS NULL THEN 1
                                                           ELSE 0 END AS new_session
                                                FROM (SELECT session_id,
                                                             {event_table_id} AS message_id,
                                                             timestamp,
                                                             {event_column} AS value,
                                                             LAG(timestamp)
                                                             OVER (PARTITION BY session_id ORDER BY timestamp) AS source_timestamp
                                                      FROM {event_table} INNER JOIN public.sessions USING (session_id)
                                                      WHERE {" AND ".join(pg_sub_query_subset)}
                                                     ) AS related_events) AS ranked_events) AS processed
                                                 {") AS marked) AS maxed WHERE timestamp >= max) AS filtered" if event_start else ""}
                                                 ) AS sorted_events
                              WHERE event_number <= %(JOURNEY_DEPTH)s) AS final
                        WHERE source_event IS NOT NULL
                          and target_event IS NOT NULL
                        GROUP BY source_event, target_event
                        ORDER BY value DESC
                        LIMIT 20;"""
        params = {"project_id": project_id, "startTimestamp": startTimestamp,
                  "endTimestamp": endTimestamp, "event_start": event_start, "JOURNEY_DEPTH": JOURNEY_DEPTH,
                  **__get_constraint_values(args), **extra_values}
        # print(cur.mogrify(pg_query, params))
        cur.execute(cur.mogrify(pg_query, params))
        rows = cur.fetchall()

    return __transform_journey(rows)


def __compute_weekly_percentage(rows):
    if rows is None or len(rows) == 0:
        return rows
    t = -1
    for r in rows:
        if r["week"] == 0:
            t = r["usersCount"]
        r["percentage"] = r["usersCount"] / t
    return rows


def __complete_retention(rows, start_date, end_date=None):
    if rows is None:
        return []
    max_week = 10
    for i in range(max_week):
        if end_date is not None and start_date + i * TimeUTC.MS_WEEK >= end_date:
            break
        neutral = {
            "firstConnexionWeek": start_date,
            "week": i,
            "usersCount": 0,
            "connectedUsers": [],
            "percentage": 0
        }
        if i < len(rows) \
                and i != rows[i]["week"]:
            rows.insert(i, neutral)
        elif i >= len(rows):
            rows.append(neutral)
    return rows


def __complete_acquisition(rows, start_date, end_date=None):
    if rows is None:
        return []
    max_week = 10
    week = 0
    delta_date = 0
    while max_week > 0:
        start_date += TimeUTC.MS_WEEK
        if end_date is not None and start_date >= end_date:
            break
        delta = 0
        if delta_date + week >= len(rows) \
                or delta_date + week < len(rows) and rows[delta_date + week]["firstConnexionWeek"] > start_date:
            for i in range(max_week):
                if end_date is not None and start_date + i * TimeUTC.MS_WEEK >= end_date:
                    break

                neutral = {
                    "firstConnexionWeek": start_date,
                    "week": i,
                    "usersCount": 0,
                    "connectedUsers": [],
                    "percentage": 0
                }
                rows.insert(delta_date + week + i, neutral)
                delta = i
        else:
            for i in range(max_week):
                if end_date is not None and start_date + i * TimeUTC.MS_WEEK >= end_date:
                    break

                neutral = {
                    "firstConnexionWeek": start_date,
                    "week": i,
                    "usersCount": 0,
                    "connectedUsers": [],
                    "percentage": 0
                }
                if delta_date + week + i < len(rows) \
                        and i != rows[delta_date + week + i]["week"]:
                    rows.insert(delta_date + week + i, neutral)
                elif delta_date + week + i >= len(rows):
                    rows.append(neutral)
                delta = i
        week += delta
        max_week -= 1
        delta_date += 1
    return rows


@dev.timed
def get_users_retention(project_id, startTimestamp=TimeUTC.now(delta_days=-70), endTimestamp=TimeUTC.now(), filters=[],
                        **args):
    startTimestamp = TimeUTC.trunc_week(startTimestamp)
    endTimestamp = startTimestamp + 10 * TimeUTC.MS_WEEK
    pg_sub_query = __get_constraints(project_id=project_id, data=args, duration=True, main_table="sessions",
                                     time_constraint=True)
    pg_sub_query.append("user_id IS NOT NULL")
    pg_sub_query.append("DATE_TRUNC('week', to_timestamp(start_ts / 1000)) = to_timestamp(%(startTimestamp)s / 1000)")
    with pg_client.PostgresClient() as cur:
        pg_query = f"""SELECT FLOOR(DATE_PART('day', connexion_week - DATE_TRUNC('week', to_timestamp(%(startTimestamp)s / 1000)::timestamp)) / 7)::integer AS week,
                               COUNT(DISTINCT connexions_list.user_id)                                     AS users_count,
                               ARRAY_AGG(DISTINCT connexions_list.user_id)                                 AS connected_users
                        FROM (SELECT DISTINCT user_id
                              FROM sessions
                              WHERE {" AND ".join(pg_sub_query)} 
                                AND NOT EXISTS((SELECT 1
                                                FROM sessions AS bsess
                                                WHERE bsess.start_ts < %(startTimestamp)s
                                                  AND project_id =  %(project_id)s
                                                  AND bsess.user_id = sessions.user_id
                                                LIMIT 1))
                              GROUP BY user_id) AS users_list
                                 LEFT JOIN LATERAL (SELECT DATE_TRUNC('week', to_timestamp(start_ts / 1000)::timestamp) AS connexion_week,
                                                           user_id
                                                    FROM sessions
                                                    WHERE users_list.user_id = sessions.user_id
                                                      AND %(startTimestamp)s <=sessions.start_ts
                                                      AND sessions.project_id =  %(project_id)s
                                                      AND sessions.start_ts < (%(endTimestamp)s - 1)
                                                    GROUP BY connexion_week, user_id
                            ) AS connexions_list ON (TRUE)
                        GROUP BY week
                        ORDER BY  week;"""

        params = {"project_id": project_id, "startTimestamp": startTimestamp,
                  "endTimestamp": endTimestamp, **__get_constraint_values(args)}
        print(cur.mogrify(pg_query, params))
        cur.execute(cur.mogrify(pg_query, params))
        rows = cur.fetchall()
        rows = __compute_weekly_percentage(helper.list_to_camel_case(rows))
    return __complete_retention(rows=rows, start_date=startTimestamp, end_date=TimeUTC.now())


@dev.timed
def get_users_acquisition(project_id, startTimestamp=TimeUTC.now(delta_days=-70), endTimestamp=TimeUTC.now(),
                          filters=[],
                          **args):
    startTimestamp = TimeUTC.trunc_week(startTimestamp)
    endTimestamp = startTimestamp + 10 * TimeUTC.MS_WEEK
    pg_sub_query = __get_constraints(project_id=project_id, data=args, duration=True, main_table="sessions",
                                     time_constraint=True)
    pg_sub_query.append("user_id IS NOT NULL")
    with pg_client.PostgresClient() as cur:
        pg_query = f"""SELECT EXTRACT(EPOCH FROM first_connexion_week::date)::bigint*1000 AS first_connexion_week,
                               FLOOR(DATE_PART('day', connexion_week - first_connexion_week) / 7)::integer AS week,
                               COUNT(DISTINCT connexions_list.user_id)                            AS users_count,
                               ARRAY_AGG(DISTINCT connexions_list.user_id)                        AS connected_users
                        FROM (SELECT DISTINCT user_id, MIN(DATE_TRUNC('week', to_timestamp(start_ts / 1000))) AS first_connexion_week
                              FROM sessions
                              WHERE {" AND ".join(pg_sub_query)} 
                                AND NOT EXISTS((SELECT 1
                                                FROM sessions AS bsess
                                                WHERE bsess.start_ts<%(startTimestamp)s
                                                  AND project_id = %(project_id)s
                                                  AND bsess.user_id = sessions.user_id
                                                LIMIT 1))
                              GROUP BY user_id) AS users_list
                                 LEFT JOIN LATERAL (SELECT DATE_TRUNC('week', to_timestamp(start_ts / 1000)::timestamp) AS connexion_week,
                                                           user_id
                                                    FROM sessions
                                                    WHERE users_list.user_id = sessions.user_id
                                                      AND first_connexion_week <=
                                                          DATE_TRUNC('week', to_timestamp(sessions.start_ts / 1000)::timestamp)
                                                      AND sessions.project_id = 1
                                                      AND sessions.start_ts < (%(endTimestamp)s - 1)
                                                    GROUP BY connexion_week, user_id) AS connexions_list ON (TRUE)
                        GROUP BY first_connexion_week, week
                        ORDER BY first_connexion_week, week;"""

        params = {"project_id": project_id, "startTimestamp": startTimestamp,
                  "endTimestamp": endTimestamp, **__get_constraint_values(args)}
        # print(cur.mogrify(pg_query, params))
        cur.execute(cur.mogrify(pg_query, params))
        rows = cur.fetchall()
        rows = __compute_weekly_percentage(helper.list_to_camel_case(rows))
    return __complete_acquisition(rows=rows, start_date=startTimestamp, end_date=TimeUTC.now())


@dev.timed
def get_feature_acquisition(project_id, startTimestamp=TimeUTC.now(delta_days=-70), endTimestamp=TimeUTC.now(),
                            filters=[],
                            **args):
    startTimestamp = TimeUTC.trunc_week(startTimestamp)
    endTimestamp = startTimestamp + 10 * TimeUTC.MS_WEEK
    pg_sub_query = __get_constraints(project_id=project_id, data=args, duration=True, main_table="sessions",
                                     time_constraint=True)
    pg_sub_query.append("user_id IS NOT NULL")
    pg_sub_query.append("feature.timestamp >= %(startTimestamp)s")
    pg_sub_query.append("feature.timestamp < %(endTimestamp)s")
    event_table = JOURNEY_TYPES["PAGES"]["table"]
    event_column = JOURNEY_TYPES["PAGES"]["column"]
    extra_values = {"value": "/"}
    default = True
    for f in filters:
        if f["type"] == "EVENT_TYPE" and JOURNEY_TYPES.get(f["value"]):
            event_table = JOURNEY_TYPES[f["value"]]["table"]
            event_column = JOURNEY_TYPES[f["value"]]["column"]
        elif f["type"] in [sessions_metas.meta_type.USERID, sessions_metas.meta_type.USERID_IOS]:
            pg_sub_query.append(f"sessions.user_id = %(user_id)s")
            extra_values["user_id"] = f["value"]
        # TODO: This will change later when the search is clear
        default = False
        extra_values["value"] = f["value"]
    pg_sub_query.append(f"feature.{event_column} = %(value)s")

    with pg_client.PostgresClient() as cur:
        if default:
            # get most used value
            pg_query = f"""SELECT {event_column} AS value, COUNT(*) AS count
                        FROM {event_table} AS feature INNER JOIN public.sessions USING (session_id)
                        WHERE {" AND ".join(pg_sub_query[:-1])}
                                AND length({event_column}) > 2
                        GROUP BY value
                        ORDER BY count DESC
                        LIMIT 1;"""
            params = {"project_id": project_id, "startTimestamp": startTimestamp,
                      "endTimestamp": endTimestamp, **__get_constraint_values(args), **extra_values}
            cur.execute(cur.mogrify(pg_query, params))
            row = cur.fetchone()
            if row is not None:
                extra_values["value"] = row["value"]

        pg_query = f"""SELECT EXTRACT(EPOCH FROM first_connexion_week::date)::bigint*1000 AS first_connexion_week,
                               FLOOR(DATE_PART('day', connexion_week - first_connexion_week) / 7)::integer AS week,
                               COUNT(DISTINCT connexions_list.user_id)                            AS users_count,
                               ARRAY_AGG(DISTINCT connexions_list.user_id)                        AS connected_users
                        FROM (SELECT user_id, DATE_TRUNC('week', to_timestamp(first_connexion_week / 1000)) AS first_connexion_week
                              FROM(SELECT DISTINCT user_id, MIN(start_ts) AS first_connexion_week
                                      FROM sessions INNER JOIN {event_table} AS feature USING (session_id)
                                      WHERE {" AND ".join(pg_sub_query)}
                                        AND user_id IS NOT NULL 
                                        AND NOT EXISTS((SELECT 1
                                                        FROM sessions AS bsess INNER JOIN {event_table} AS bfeature USING (session_id)
                                                        WHERE bsess.start_ts<%(startTimestamp)s
                                                          AND project_id = %(project_id)s
                                                          AND bsess.user_id = sessions.user_id
                                                          AND bfeature.timestamp<%(startTimestamp)s
                                                          AND bfeature.{event_column}=%(value)s
                                                        LIMIT 1))
                                      GROUP BY user_id) AS raw_users_list) AS users_list
                                 LEFT JOIN LATERAL (SELECT DATE_TRUNC('week', to_timestamp(start_ts / 1000)::timestamp) AS connexion_week,
                                                           user_id
                                                    FROM sessions INNER JOIN {event_table} AS feature USING(session_id)
                                                    WHERE users_list.user_id = sessions.user_id
                                                      AND first_connexion_week <=
                                                          DATE_TRUNC('week', to_timestamp(sessions.start_ts / 1000)::timestamp)
                                                      AND sessions.project_id = 1
                                                      AND sessions.start_ts < (%(endTimestamp)s - 1)
                                                      AND feature.timestamp >= %(startTimestamp)s
                                                      AND feature.timestamp < %(endTimestamp)s
                                                      AND feature.{event_column} = %(value)s
                                                    GROUP BY connexion_week, user_id) AS connexions_list ON (TRUE)
                        GROUP BY first_connexion_week, week
                        ORDER BY first_connexion_week, week;"""

        params = {"project_id": project_id, "startTimestamp": startTimestamp,
                  "endTimestamp": endTimestamp, **__get_constraint_values(args), **extra_values}
        # print(cur.mogrify(pg_query, params))
        cur.execute(cur.mogrify(pg_query, params))
        rows = cur.fetchall()
        rows = __compute_weekly_percentage(helper.list_to_camel_case(rows))
    return __complete_acquisition(rows=rows, start_date=startTimestamp, end_date=TimeUTC.now())


@dev.timed
def feature_popularity_frequency(project_id, startTimestamp=TimeUTC.now(delta_days=-70), endTimestamp=TimeUTC.now(),
                                 filters=[],
                                 **args):
    startTimestamp = TimeUTC.trunc_week(startTimestamp)
    endTimestamp = startTimestamp + 10 * TimeUTC.MS_WEEK
    pg_sub_query = __get_constraints(project_id=project_id, data=args, duration=True, main_table="sessions",
                                     time_constraint=True)
    event_table = JOURNEY_TYPES["CLICK"]["table"]
    event_column = JOURNEY_TYPES["CLICK"]["column"]
    for f in filters:
        if f["type"] == "EVENT_TYPE" and JOURNEY_TYPES.get(f["value"]):
            event_table = JOURNEY_TYPES[f["value"]]["table"]
            event_column = JOURNEY_TYPES[f["value"]]["column"]
        elif f["type"] in [sessions_metas.meta_type.USERID, sessions_metas.meta_type.USERID_IOS]:
            pg_sub_query.append(f"sessions.user_id = %(user_id)s")

    with pg_client.PostgresClient() as cur:
        pg_query = f"""SELECT  COUNT(DISTINCT user_id) AS count
                        FROM sessions
                        WHERE {" AND ".join(pg_sub_query)}
                            AND user_id IS NOT NULL;"""
        params = {"project_id": project_id, "startTimestamp": startTimestamp,
                  "endTimestamp": endTimestamp, **__get_constraint_values(args)}
        # print(cur.mogrify(pg_query, params))
        # print("---------------------")
        cur.execute(cur.mogrify(pg_query, params))
        all_user_count = cur.fetchone()["count"]
        if all_user_count == 0:
            return []
        pg_sub_query.append("feature.timestamp >= %(startTimestamp)s")
        pg_sub_query.append("feature.timestamp < %(endTimestamp)s")
        pg_sub_query.append(f"length({event_column})>2")
        pg_query = f"""SELECT {event_column} AS value, COUNT(DISTINCT user_id) AS count
                    FROM {event_table} AS feature INNER JOIN sessions USING (session_id)
                    WHERE {" AND ".join(pg_sub_query)}
                        AND user_id IS NOT NULL
                    GROUP BY value
                    ORDER BY count DESC
                    LIMIT 7;"""
        # print(cur.mogrify(pg_query, params))
        # print("---------------------")
        cur.execute(cur.mogrify(pg_query, params))
        popularity = cur.fetchall()
        pg_query = f"""SELECT {event_column} AS value, COUNT(session_id) AS count
                        FROM {event_table} AS feature INNER JOIN sessions USING (session_id)
                        WHERE {" AND ".join(pg_sub_query)}
                        GROUP BY value;"""
        # print(cur.mogrify(pg_query, params))
        # print("---------------------")
        cur.execute(cur.mogrify(pg_query, params))
        frequencies = cur.fetchall()
        total_usage = sum([f["count"] for f in frequencies])
        frequencies = {f["value"]: f["count"] for f in frequencies}
        for p in popularity:
            p["popularity"] = p.pop("count") / all_user_count
            p["frequency"] = frequencies[p["value"]] / total_usage

    return popularity