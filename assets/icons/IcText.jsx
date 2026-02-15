import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcText = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M20 3H4c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1s1-.45 1-1V5h6v14H9c-.55 0-1 .45-1 1s.45 1 1 1h6c.55 0 1-.45 1-1s-.45-1-1-1h-2V5h6v2c0 .55.45 1 1 1s1-.45 1-1V4c0-.55-.45-1-1-1z"
      fill="currentColor"
     />
    </RnSvg>);
};
