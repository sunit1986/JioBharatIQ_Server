import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcArrowBack = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M2.29 12.71l6 6a1.004 1.004 0 101.42-1.42L5.41 13H21a1 1 0 100-2H5.41l4.3-4.29a1 1 0 000-1.42 1 1 0 00-1.42 0l-6 6a1 1 0 000 1.42z"
      fill="currentColor"
     />
    </RnSvg>);
};
