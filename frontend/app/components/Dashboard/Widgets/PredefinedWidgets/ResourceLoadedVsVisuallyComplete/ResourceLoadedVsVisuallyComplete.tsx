import React from 'react';
import { NoContent } from 'UI';
import { Styles } from '../../common';
import { 
  ComposedChart, Bar, CartesianGrid, Line, Legend, ResponsiveContainer, 
  XAxis, YAxis, Tooltip
} from 'recharts';

interface Props {
    data: any
}
function ResourceLoadedVsVisuallyComplete(props: Props) {
    const { data } = props;
    const gradientDef = Styles.gradientDef();
    const params = { density: 70 }

    return (
        <NoContent
          size="small"
          show={ data.chart.length === 0 }
        >
          <ResponsiveContainer height={ 240 } width="100%">
            <ComposedChart
                data={data.chart}
                margin={ Styles.chartMargins}
              >
                <CartesianGrid strokeDasharray="3 3" vertical={ false } stroke="#EEEEEE" />
                <XAxis
                  {...Styles.xaxis}
                  dataKey="time"
                  // interval={3}
                  interval={(params.density / 7)}
                />
                <YAxis
                  {...Styles.yaxis}
                  label={{ ...Styles.axisLabelLeft, value: "Visually Complete (ms)" }}
                  yAxisId="left"
                  tickFormatter={val => Styles.tickFormatter(val, 'ms')}
                />
                <YAxis
                  {...Styles.yaxis}
                  label={{
                    ...Styles.axisLabelLeft,
                    value: "Number of Resources",
                    position: "insideRight",
                    offset: 0
                  }}
                  yAxisId="right"
                  orientation="right"
                  tickFormatter={val => Styles.tickFormatter(val)}
                />
                <Tooltip {...Styles.tooltip} />
                <Legend />
                <Bar minPointSize={1} yAxisId="right" name="Images" type="monotone" dataKey="types.img" stackId="a" fill={Styles.colors[0]} />
                <Bar yAxisId="right" name="Scripts" type="monotone" dataKey="types.script" stackId="a" fill={Styles.colors[2]} />
                <Bar yAxisId="right" name="CSS" type="monotone" dataKey="types.stylesheet" stackId="a" fill={Styles.colors[4]} />
                <Line
                  yAxisId="left"
                  name="Visually Complete"
                  type="monotone"
                  dataKey="avgTimeToRender"
                  stroke={Styles.lineColor }
                  dot={false}
                  unit=" ms"
                  strokeWidth={2}
                />
              </ComposedChart>
          </ResponsiveContainer>
        </NoContent>
    );
}

export default ResourceLoadedVsVisuallyComplete;