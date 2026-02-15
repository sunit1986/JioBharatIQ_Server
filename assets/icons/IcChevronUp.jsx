import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcChevronUp = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M16 15a.998.998 0 01-.71-.29L12 11.41l-3.29 3.3a1.004 1.004 0 01-1.42-1.42l4-4a.999.999 0 011.42 0l4 4A1.001 1.001 0 0116 15z"
      fill="currentColor"
     />
    </RnSvg>);
};
