import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcInfo = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 3.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3zm2 12h-4a1 1 0 010-2h1v-3h-1a1 1 0 010-2h2a1 1 0 011 1v4h1a1 1 0 010 2z"
      fill="currentColor"
     />
    </RnSvg>);
};
