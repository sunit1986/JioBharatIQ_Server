import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcList = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M20 17H9a1 1 0 000 2h11a1 1 0 000-2zm0-6H9a1 1 0 000 2h11a1 1 0 000-2zM9 7h11a1 1 0 100-2H9a1 1 0 000 2zM4.5 4.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm0 6a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm0 6a1.5 1.5 0 100 3 1.5 1.5 0 000-3z"
      fill="currentColor"
     />
    </RnSvg>);
};
