import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcShare = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M18 15a3 3 0 00-2.15.91L8 12.27c.005-.09.005-.18 0-.27.005-.09.005-.18 0-.27l7.88-3.64A3 3 0 1015 6c-.005.09-.005.18 0 .27L7.15 9.91a3 3 0 100 4.18L15 17.73c-.005.09-.005.18 0 .27a3 3 0 103-3z"
      fill="currentColor"
     />
    </RnSvg>);
};
