import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcRefresh = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M12 4a8 8 0 013.85 1H15a1 1 0 100 2h3a1 1 0 001-1V3a1 1 0 00-2 0v.36A10 10 0 0012 2a10 10 0 00-8.65 5A9.94 9.94 0 002 12a1 1 0 102 0 8 8 0 018-8zm9.71 7.29A1 1 0 0020 12a8 8 0 01-11.84 7H9a1 1 0 000-2H6a1 1 0 00-1 1v3a1 1 0 102 0v-.36A10 10 0 0012 22a10 10 0 0010-10 1 1 0 00-.29-.71z"
      fill="currentColor"
     />
    </RnSvg>);
};
