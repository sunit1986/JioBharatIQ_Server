import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcMinus = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M3.293 11.293A1 1 0 014 11h16a1 1 0 010 2H4a1 1 0 01-.707-1.707z"
      fill="currentColor"
     />
    </RnSvg>);
};
