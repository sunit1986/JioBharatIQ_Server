import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcProfile = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M16 6a4 4 0 11-8 0 4 4 0 018 0zm4 10.5c0 3.038-3.582 5.5-8 5.5s-8-2.462-8-5.5S7.582 11 12 11s8 2.462 8 5.5z"
      fill="currentColor"
     />
    </RnSvg>);
};
