import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcTime = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M12 2a10 10 0 100 20 10 10 0 000-20zm1 11a1 1 0 01-1 1H9a1 1 0 010-2h2V9a1 1 0 012 0v4z"
      fill="currentColor"
     />
    </RnSvg>);
};
