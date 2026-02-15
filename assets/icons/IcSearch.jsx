import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcSearch = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M10.004 2a7 7 0 015.6 11.19l6.11 6.1a1.002 1.002 0 01-.325 1.639.999.999 0 01-1.095-.219l-6.1-6.11A7 7 0 1110.004 2zm0 12a5 5 0 100-10 5 5 0 000 10z"
      fill="currentColor"
     />
    </RnSvg>);
};
