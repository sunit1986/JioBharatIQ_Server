import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcChevronRight = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M10 17a1.002 1.002 0 01-1.006-1 1 1 0 01.296-.71l3.3-3.29-3.3-3.29a1.004 1.004 0 011.42-1.42l4 4a.997.997 0 01.219 1.095.999.999 0 01-.22.325l-4 4A1 1 0 0110 17z"
      fill="currentColor"
     />
    </RnSvg>);
};
