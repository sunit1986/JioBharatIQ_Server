import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcCopy = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M13 8H5a3 3 0 00-3 3v8a3 3 0 003 3h8a3 3 0 003-3v-8a3 3 0 00-3-3zm6-6h-8a3 3 0 00-3 3v1h5a5 5 0 015 5v5h1a3 3 0 003-3V5a3 3 0 00-3-3z"
      fill="currentColor"
     />
    </RnSvg>);
};
