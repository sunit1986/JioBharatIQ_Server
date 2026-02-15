import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcChevronLeft = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M14 17a1.003 1.003 0 01-.71-.29l-4-4a1 1 0 010-1.42l4-4a1.005 1.005 0 011.42 1.42L11.41 12l3.3 3.29a.997.997 0 01.219 1.095.999.999 0 01-.93.615z"
      fill="currentColor"
     />
    </RnSvg>);
};
