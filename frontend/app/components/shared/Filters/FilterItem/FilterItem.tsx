import React from 'react';
import FilterOperator from '../FilterOperator/FilterOperator';
import FilterSelection from '../FilterSelection';
import FilterValue from '../FilterValue';
import { Icon } from 'UI';

interface Props {
  filterIndex: number;
  filter: any; // event/filter
  onUpdate: (filter) => void;
  onRemoveFilter: () => void;
}
function FitlerItem(props: Props) {
  const { filterIndex, filter, onUpdate } = props;

  const replaceFilter = (filter) => {
    onUpdate(filter);
  };

  const onAddValue = () => {
    const newValues = filter.value.concat("")
    onUpdate({ ...filter, value: newValues })
  }

  const onRemoveValue = (valueIndex) => {
    const newValues = filter.value.filter((_, _index) => _index !== valueIndex)
    onUpdate({ ...filter, value: newValues })
  }

  const onSelect = (e, item, valueIndex) => {
    const newValues = filter.value.map((_, _index) => {
      if (_index === valueIndex) {
        return item.value;
      }
      return _;
    })
    onUpdate({ ...filter, value: newValues })
  }

  console.log('filter', filter);

  const onOperatorChange = (e, { name, value }) => {
    onUpdate({ ...filter, operator: value })
  }

  return (
    <div className="flex items-center mb-4">
      <div className="flex items-start mr-auto">
        <div className="mt-1 w-6 h-6 text-xs flex justify-center rounded-full bg-gray-light-shade mr-2">{filterIndex+1}</div>
        <FilterSelection filter={filter} onFilterClick={replaceFilter} />
        <FilterOperator filter={filter} onChange={onOperatorChange} className="mx-2 flex-shrink-0"/>
        <div className="grid grid-cols-3 gap-3">
          {filter.value && filter.value.map((value, valueIndex) => (
            <FilterValue
              showCloseButton={filter.value.length > 1}
              showOrButton={valueIndex === filter.value.length - 1}
              // filter={filter}
              // key={valueIndex}
              value={value}
              key={filter.key}
              index={valueIndex}
              onAddValue={onAddValue}
              onRemoveValue={() => onRemoveValue(valueIndex)}
              onSelect={(e, item) => onSelect(e, item, valueIndex)}
            />
          ))}
        </div>
      </div>
      <div className="flex self-start mt-2">
        <div
          className="cursor-pointer"
          onClick={props.onRemoveFilter}
        > 
          <Icon name="close" size="18" />
        </div>
      </div>
    </div>
  );
}

export default FitlerItem;