import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcStop = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M16.84 4H7.16A3.16 3.16 0 004 7.16v9.68A3.16 3.16 0 007.16 20h9.68A3.16 3.16 0 0020 16.84V7.16A3.16 3.16 0 0016.84 4z"
      fill="currentColor"
     />
    </RnSvg>);
};
