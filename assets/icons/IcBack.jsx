import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcBack = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M15 20a1.003 1.003 0 01-.71-.29l-7-7a1 1 0 010-1.42l7-7a1.005 1.005 0 011.42 1.42L9.41 12l6.3 6.29a.997.997 0 01.219 1.095.999.999 0 01-.93.615z"
      fill="currentColor"
     />
    </RnSvg>);
};
