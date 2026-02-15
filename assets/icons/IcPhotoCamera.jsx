import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcPhotoCamera = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M19 6h-7V5a1 1 0 00-1-1H7a1 1 0 00-1 1v1H5a3.12 3.12 0 00-3 3.23v7.54A3.12 3.12 0 005 20h14a3.12 3.12 0 003-3.23V9.23A3.12 3.12 0 0019 6zm-7 10a3 3 0 110-5.999A3 3 0 0112 16z"
      fill="currentColor"
     />
    </RnSvg>);
};
