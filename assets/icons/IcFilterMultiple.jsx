import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcFilterMultiple = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M4 7h9.18a3 3 0 005.64 0H20a1 1 0 100-2h-1.18a3 3 0 00-5.64 0H4a1 1 0 000 2zm12-2a1 1 0 110 2 1 1 0 010-2zm4 12h-1.18a3 3 0 00-5.64 0H4a1 1 0 000 2h9.18a3 3 0 005.64 0H20a1 1 0 100-2zm-4 2a1 1 0 110-2 1 1 0 010 2zm4-8h-9.18a3 3 0 00-5.64 0H4a1 1 0 000 2h1.18a3 3 0 005.64 0H20a1 1 0 100-2zM8 13a1 1 0 110-2 1 1 0 010 2z"
      fill="currentColor"
     />
    </RnSvg>);
};
