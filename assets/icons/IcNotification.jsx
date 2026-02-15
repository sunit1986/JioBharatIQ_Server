import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcNotification = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M21 16h-1v-6a8 8 0 00-16 0v6H3a1 1 0 000 2h18a1 1 0 000-2zm-9 6a3 3 0 003-3H9a3 3 0 003 3z"
      fill="currentColor"
     />
    </RnSvg>);
};
