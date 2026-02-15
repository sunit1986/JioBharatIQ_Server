import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcClose = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M13.41 12l6.3-6.29a1.004 1.004 0 00-1.42-1.42L12 10.59l-6.29-6.3a1.004 1.004 0 10-1.42 1.42l6.3 6.29-6.3 6.29a.999.999 0 000 1.42 1 1 0 001.42 0l6.29-6.3 6.29 6.3a1.001 1.001 0 001.639-.325 1 1 0 00-.22-1.095L13.41 12z"
      fill="currentColor"
     />
    </RnSvg>);
};
