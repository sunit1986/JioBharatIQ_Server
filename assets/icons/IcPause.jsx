import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcPause = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M8.5 4A1.5 1.5 0 007 5.5v13a1.5 1.5 0 003 0v-13A1.5 1.5 0 008.5 4zm7 0A1.5 1.5 0 0014 5.5v13a1.5 1.5 0 103 0v-13A1.5 1.5 0 0015.5 4z"
      fill="currentColor"
     />
    </RnSvg>);
};
