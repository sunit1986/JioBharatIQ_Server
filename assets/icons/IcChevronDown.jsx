import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcChevronDown = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M12 15a1.002 1.002 0 01-.71-.29l-4-4a1.004 1.004 0 111.42-1.42l3.29 3.3 3.29-3.3a1.004 1.004 0 111.42 1.42l-4 4A1.001 1.001 0 0112 15z"
      fill="currentColor"
     />
    </RnSvg>);
};
