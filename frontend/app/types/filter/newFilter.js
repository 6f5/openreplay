import Record from 'Types/Record';

const CLICK = 'CLICK';
const INPUT = 'INPUT';
const LOCATION = 'LOCATION';
const VIEW = 'VIEW_IOS';
const CONSOLE = 'ERROR';
const METADATA = 'METADATA';
const CUSTOM = 'CUSTOM';
const URL = 'URL';
const CLICK_RAGE = 'CLICKRAGE';
const USER_BROWSER  = 'USERBROWSER';
const USER_OS = 'USEROS';
const USER_COUNTRY  = 'USERCOUNTRY';
const USER_DEVICE = 'USERDEVICE';
const PLATFORM = 'PLATFORM';
const DURATION  = 'DURATION';
const REFERRER  = 'REFERRER';
const ERROR = 'ERROR';
const MISSING_RESOURCE = 'MISSINGRESOURCE';
const SLOW_SESSION = 'SLOWSESSION';
const JOURNEY = 'JOUNRNEY';
const FETCH = 'REQUEST';
const GRAPHQL = 'GRAPHQL';
const STATEACTION = 'STATEACTION';
const REVID = 'REVID';
const USERANONYMOUSID = 'USERANONYMOUSID';
const USERID = 'USERID';

const ISSUE = 'ISSUE';
const EVENTS_COUNT = 'EVENTS_COUNT';
const UTM_SOURCE = 'UTM_SOURCE';
const UTM_MEDIUM = 'UTM_MEDIUM';
const UTM_CAMPAIGN = 'UTM_CAMPAIGN';


const DOM_COMPLETE = 'DOM_COMPLETE';
const LARGEST_CONTENTFUL_PAINT_TIME = 'LARGEST_CONTENTFUL_PAINT_TIME';
const TIME_BETWEEN_EVENTS = 'TIME_BETWEEN_EVENTS';
const TTFB = 'TTFB';
const AVG_CPU_LOAD = 'AVG_CPU_LOAD';
const AVG_MEMORY_USAGE = 'AVG_MEMORY_USAGE';

export const TYPES = {
  ERROR,
  MISSING_RESOURCE,
  SLOW_SESSION,
  CLICK_RAGE,
  CLICK,
  INPUT,
  LOCATION,
  VIEW,
  CONSOLE,
  METADATA,
  CUSTOM,
  URL,
  USER_BROWSER,
  USER_OS,
  USER_DEVICE,
  PLATFORM,
  DURATION,
  REFERRER,
  USER_COUNTRY,
  JOURNEY,
  FETCH,
  GRAPHQL,
  STATEACTION,
  REVID,
  USERANONYMOUSID,
  USERID,
  ISSUE,
  EVENTS_COUNT,
  UTM_SOURCE,
  UTM_MEDIUM,
  UTM_CAMPAIGN,
  
  DOM_COMPLETE,
  LARGEST_CONTENTFUL_PAINT_TIME,
  TIME_BETWEEN_EVENTS,
  TTFB,
  AVG_CPU_LOAD,
  AVG_MEMORY_USAGE,
};

const filterKeys = ['is', 'isNot'];
const stringFilterKeys = ['is', 'isNot', 'contains', 'startsWith', 'endsWith'];
const targetFilterKeys = ['on', 'notOn'];
const signUpStatusFilterKeys = ['isSignedUp', 'notSignedUp'];
const rangeFilterKeys = ['before', 'after', 'on', 'inRange', 'notInRange', 'withInLast', 'notWithInLast'];

const options = [
  {
    key: 'is',
    text: 'is',
    value: 'is'
  }, {
    key: 'isNot',
    text: 'is not',
    value: 'isNot'
  }, {
    key: 'startsWith',
    text: 'starts with',
    value: 'startsWith'
  }, {
    key: 'endsWith',
    text: 'ends with',
    value: 'endsWith'
  }, {
    key: 'contains',
    text: 'contains',
    value: 'contains'
  }, {
    key: 'doesNotContain',
    text: 'does not contain',
    value: 'doesNotContain'
  }, {
    key: 'hasAnyValue',
    text: 'has any value',
    value: 'hasAnyValue'
  }, {
    key: 'hasNoValue',
    text: 'has no value',
    value: 'hasNoValue'
  }, 
  

  {
    key: 'isSignedUp',
    text: 'is signed up',
    value: 'isSignedUp'
  }, {
    key: 'notSignedUp',
    text: 'not signed up',
    value: 'notSignedUp'
  },
  
  
  {
    key: 'before',
    text: 'before',
    value: 'before'
  }, {
    key: 'after',
    text: 'after',
    value: 'after'
  }, {
    key: 'on',
    text: 'on',
    value: 'on'
  }, {
    key: 'notOn',
    text: 'not on',
    value: 'notOn'
  }, {
    key: 'inRage',
    text: 'in rage',
    value: 'inRage'
  }, {
    key: 'notInRage',
    text: 'not in rage',
    value: 'notInRage'
  }, {
    key: 'withinLast',
    text: 'within last',
    value: 'withinLast'
  }, {
    key: 'notWithinLast',
    text: 'not within last',
    value: 'notWithinLast'
  },

  {
    key: 'greaterThan',
    text: 'greater than',
    value: 'greaterThan'
  }, {
    key: 'lessThan',
    text: 'less than',
    value: 'lessThan'
  }, {
    key: 'equal',
    text: 'equal',
    value: 'equal'
  }, {
    key: 'not equal',
    text: 'not equal',
    value: 'not equal'
  },


  {
    key: 'onSelector',
    text: 'on selector',
    value: 'onSelector'
  }, {
    key: 'onText',
    text: 'on text',
    value: 'onText'
  }, {
    key: 'onComponent',
    text: 'on component',
    value: 'onComponent'
  },


  {
    key: 'onAnything',
    text: 'on anything',
    value: 'onAnything'
  }
];

export const filterOptions = options.filter(({key}) => filterKeys.includes(key));
export const stringFilterOptions = options.filter(({key}) => stringFilterKeys.includes(key));
export const targetFilterOptions = options.filter(({key}) => targetFilterKeys.includes(key));
export const booleanOptions = [
  { key: 'true', text: 'true', value: 'true' },
  { key: 'false', text: 'false', value: 'false' },
]

export const filtersMap = {
  [TYPES.CLICK]: { key: TYPES.CLICK, type: 'multiple', category: 'interactions', label: 'Click', operator: 'on', operatorOptions: targetFilterOptions, icon: 'filters/click', isEvent: true },
  [TYPES.INPUT]: { key: TYPES.INPUT, type: 'multiple', category: 'interactions', label: 'Input', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click', isEvent: true },
  [TYPES.LOCATION]: { key: TYPES.LOCATION, type: 'multiple', category: 'interactions', label: 'Page', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click', isEvent: true },

  [TYPES.USER_OS]: { key: TYPES.USER_OS, type: 'multiple', category: 'gear', label: 'User OS', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.USER_BROWSER]: { key: TYPES.USER_BROWSER, type: 'multiple', category: 'gear', label: 'User Browser', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.USER_DEVICE]: { key: TYPES.USER_DEVICE, type: 'multiple', category: 'gear', label: 'User Device', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.PLATFORM]: { key: TYPES.PLATFORM, type: 'multiple', category: 'gear', label: 'Platform', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.REVID]: { key: TYPES.REVID, type: 'multiple', category: 'gear', label: 'RevId', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },

  [TYPES.REFERRER]: { key: TYPES.REFERRER, type: 'multiple', category: 'recording_attributes', label: 'Referrer', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.DURATION]: { key: TYPES.DURATION, type: 'number', category: 'recording_attributes', label: 'Duration', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.USER_COUNTRY]: { key: TYPES.USER_COUNTRY, type: 'multiple', category: 'recording_attributes', label: 'User Country', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },

  [TYPES.CONSOLE]: { key: TYPES.CONSOLE, type: 'multiple', category: 'javascript', label: 'Console', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.ERROR]: { key: TYPES.ERROR, type: 'multiple', category: 'javascript', label: 'Error', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.FETCH]: { key: TYPES.FETCH, type: 'multiple', category: 'javascript', label: 'Fetch', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.GRAPHQL]: { key: TYPES.GRAPHQL, type: 'multiple', category: 'javascript', label: 'GraphQL', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.STATEACTION]: { key: TYPES.STATEACTION, type: 'multiple', category: 'javascript', label: 'StateAction', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },

  [TYPES.USERID]: { key: TYPES.USERID, type: 'multiple', category: 'user', label: 'UserId', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.USERANONYMOUSID]: { key: TYPES.USERANONYMOUSID, type: 'multiple', category: 'user', label: 'UserAnonymousId', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  
  [TYPES.DOM_COMPLETE]: { key: TYPES.DOM_COMPLETE, type: 'multiple', category: 'new', label: 'DOM Complete', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.LARGEST_CONTENTFUL_PAINT_TIME]: { key: TYPES.LARGEST_CONTENTFUL_PAINT_TIME, type: 'number', category: 'new', label: 'Largest Contentful Paint Time', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.TIME_BETWEEN_EVENTS]: { key: TYPES.TIME_BETWEEN_EVENTS, type: 'number', category: 'new', label: 'Time Between Events', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.TTFB]: { key: TYPES.TTFB, type: 'time', category: 'new', label: 'TTFB', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.AVG_CPU_LOAD]: { key: TYPES.AVG_CPU_LOAD, type: 'number', category: 'new', label: 'Avg CPU Load', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.AVG_MEMORY_USAGE]: { key: TYPES.AVG_MEMORY_USAGE, type: 'number', category: 'new', label: 'Avg Memory Usage', operator: 'is', operatorOptions: stringFilterOptions, icon: 'filters/click' },
  [TYPES.SLOW_SESSION]: { key: TYPES.SLOW_SESSION, type: 'boolean', category: 'new', label: 'Slow Session', operator: 'true', operatorOptions: [{ key: 'true', text: 'true', value: 'true' }], icon: 'filters/click' },
  [TYPES.MISSING_RESOURCE]: { key: TYPES.MISSING_RESOURCE, type: 'boolean', category: 'new', label: 'Missing Resource', operator: 'true', operatorOptions: [{ key: 'inImages', text: 'in images', value: 'true' }], icon: 'filters/click' },
  [TYPES.CLICK_RAGE]: { key: TYPES.CLICK_RAGE, type: 'boolean', category: 'new', label: 'Click Rage', operator: 'onAnything', operatorOptions: [{ key: 'onAnything', text: 'on anything', value: 'true' }], icon: 'filters/click' },
  // [TYPES.URL]: { / [TYPES,TYPES. category: 'interactions', label: 'URL', operator: 'is', operatorOptions: stringFilterOptions },
  // [TYPES.CUSTOM]: { / [TYPES,TYPES. category: 'interactions', label: 'Custom', operator: 'is', operatorOptions: stringFilterOptions },
  // [TYPES.METADATA]: { / [TYPES,TYPES. category: 'interactions', label: 'Metadata', operator: 'is', operatorOptions: stringFilterOptions },
}

export default Record({
  timestamp: 0,
  key: '',
  label: '',
  icon: '',
  type: '',
  value: [""],
  category: '',
  
  custom: '',
  // target: Target(),
  level: '',
  source: null,
  hasNoValue: false,
  isFilter: false,
  actualValue: '',
  
  operator: 'is',
  operatorOptions: [],
  isEvent: false,
  index: 0,
}, {
  keyKey: "_key",
  fromJS: ({ ...filter }) => ({
    ...filter,
    key: filter.type,
    type: filter.type, // camelCased(filter.type.toLowerCase()),
    // key: filter.type === METADATA ? filter.label : filter.key || filter.type, // || camelCased(filter.type.toLowerCase()),
    // label: getLabel(filter),
    // target: Target(target),
    // operator: getOperatorDefault(filter.type),
    // value: target ? target.label : filter.value,
    // value: typeof value === 'string' ? [value] : value,
    // icon: filter.type ? getfilterIcon(filter.type) : 'filters/metadata'
  }),
})

// const NewFilterType = (key, category, icon, isEvent = false) => {
//   return {
//     key: key,
//     category: category,
//     label: filterMap[key].label,
//     icon: icon,
//     isEvent: isEvent,
//     operators: filterMap[key].operatorOptions,
//     value: [""]
//   }
// }