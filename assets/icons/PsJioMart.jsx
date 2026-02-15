import React from 'react';
import RnSvg, { G, Rect, Path, Defs, ClipPath } from 'react-native-svg';

export const PsJioMart = (props) => {
  return (<RnSvg
      viewBox="0 0 32 32"
      fill="none"
      {...props}
    ><G
      clipPath="url(#ps_jio_mart_svg__clip0_4932_101314)"
    ><Path
      fill="#E30513"
      d="M0 0h32v32H0z"
     />
      <Path
      d="M23.39 11.65a1.998 1.998 0 00-1.48-.65H20v-1a4 4 0 10-8 0v1h-1.91a2 2 0 00-1.48.65 2.05 2.05 0 00-.52 1.52l.76 9.08a3 3 0 003 2.75h8.32a3 3 0 003-2.75l.76-9.08a2.05 2.05 0 00-.54-1.52zM14 10a2 2 0 014 0v1h-4v-1z"
      fill="#fff"
     />
    </G>
      <Defs

    ><ClipPath
      id="ps_jio_mart_svg__clip0_4932_101314"
    ><Rect
      width="32"
      height="32"
      rx="16"
      fill="#fff"
     />
    </ClipPath>
    </Defs>
    </RnSvg>);
};
