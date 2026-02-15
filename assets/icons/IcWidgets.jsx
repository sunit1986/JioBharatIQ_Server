import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcWidgets = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M9 3H5a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2V5a2 2 0 00-2-2zm0 10H5a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2v-4a2 2 0 00-2-2zm12.16-7.41l-2.75-2.75a2 2 0 00-2.82 0l-2.75 2.75a2 2 0 000 2.82l2.75 2.75a2 2 0 002.82 0l2.75-2.75a2 2 0 000-2.82zM19 13h-4a2 2 0 00-2 2v4a2 2 0 002 2h4a2 2 0 002-2v-4a2 2 0 00-2-2z"
      fill="currentColor"
     />
    </RnSvg>);
};
