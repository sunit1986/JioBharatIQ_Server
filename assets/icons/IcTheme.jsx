import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcTheme = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M19 2h-8a3 3 0 00-3 3v3H5a3 3 0 00-3 3v8a3 3 0 003 3h8a3 3 0 003-3v-3h3a3 3 0 003-3V5a3 3 0 00-3-3zm-5 17a1 1 0 01-1 1H5a1 1 0 01-1-1v-8a1 1 0 011-1h8a1 1 0 011 1v8z"
      fill="currentColor"
    >
    </Path>
    </RnSvg>);
};
