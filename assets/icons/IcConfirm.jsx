import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const IcConfirm = (props) => {
  return (<RnSvg
      viewBox="0 0 24 24"
      fill="none"
      {...props}
    ><Path
      d="M9 19a1.002 1.002 0 01-.71-.29l-5-5a1.004 1.004 0 111.42-1.42L9 16.59l10.29-10.3a1.004 1.004 0 111.42 1.42l-11 11A1 1 0 019 19z"
      fill="currentColor"
     />
    </RnSvg>);
};
