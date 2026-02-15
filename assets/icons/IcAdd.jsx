import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcAdd = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M20 11h-7V4a1 1 0 00-2 0v7H4a1 1 0 000 2h7v7a1 1 0 002 0v-7h7a1 1 0 000-2z"
      fill="currentColor"
     />
    </RnSvg>);
};
