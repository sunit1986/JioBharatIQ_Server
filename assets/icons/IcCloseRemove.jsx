import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcCloseRemove = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M12 2a10 10 0 100 20 10 10 0 000-20zm3.71 12.29a1.002 1.002 0 01-.325 1.639 1 1 0 01-1.095-.219L12 13.41l-2.29 2.3a1 1 0 01-1.639-.325 1 1 0 01.219-1.095l2.3-2.29-2.3-2.29a1.004 1.004 0 011.42-1.42l2.29 2.3 2.29-2.3a1.004 1.004 0 011.42 1.42L13.41 12l2.3 2.29z"
      fill="currentColor"
     />
    </RnSvg>);
};
