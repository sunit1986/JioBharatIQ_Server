import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcChat = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M15 4H9a7 7 0 00-1 13.92V20a1.5 1.5 0 002.4 1.2l4.27-3.2H15a7 7 0 000-14zm-7 8a1 1 0 110-2 1 1 0 010 2zm4 0a1 1 0 110-2 1 1 0 010 2zm4 0a1 1 0 110-2 1 1 0 010 2z"
      fill="currentColor"
     />
    </RnSvg>);
};
