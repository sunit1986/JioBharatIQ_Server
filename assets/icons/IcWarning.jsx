import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcWarning = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M12 2a10 10 0 100 20 10 10 0 000-20zm-1 4.5a1 1 0 012 0v6a1 1 0 01-2 0v-6zm1 12a1.5 1.5 0 110-3 1.5 1.5 0 010 3z"
      fill="currentColor"
     />
    </RnSvg>);
};
