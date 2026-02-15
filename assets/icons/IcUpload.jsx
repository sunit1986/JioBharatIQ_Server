import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcUpload = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M7.71 8.71L11 5.41V17a1 1 0 102 0V5.41l3.29 3.3a.999.999 0 001.42 0 1.001 1.001 0 000-1.42l-5-5a1 1 0 00-1.42 0l-5 5a1.004 1.004 0 101.42 1.42zM17 20H7a1 1 0 000 2h10a1 1 0 100-2z"
      fill="currentColor"
     />
    </RnSvg>);
};
