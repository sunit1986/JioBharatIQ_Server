import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcPlay = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M19.15 10.36l-10-7A2 2 0 008 3a1.88 1.88 0 00-.92.23A2 2 0 006 5v14a2 2 0 001.08 1.77c.282.154.599.233.92.23a2 2 0 001.15-.36l10-7a2 2 0 000-3.28z"
      fill="currentColor"
     />
    </RnSvg>);
};
