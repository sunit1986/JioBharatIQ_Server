import { cloneElement } from 'react';
import { pascalCase } from '@jds/utils';
import { useStyles } from '@jds/rn-engine';
import IconMap from './map.js';

export const Icon = (props: any) => {
  const value = props.value;
  const stringIcon = typeof value === 'string';
  const camelCaseIcon = !stringIcon ? value : pascalCase(value || '', '_');
  const NewIcon = IconMap[camelCaseIcon];
  const icon = NewIcon && <NewIcon />;
  if (!value) {
    return null;
  }
  const styles = useStyles(props, 'icon');
  if (icon?.$$typeof === Symbol.for('react.element')) {
    return cloneElement(icon, {
      style: styles,
      fill: styles.color,
    });
  }

  return null;
};
