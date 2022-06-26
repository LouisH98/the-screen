import { useEffect, useState } from "react";
import { getScreenData } from "../utils/ScreenAPI";
// export function PixelRow(row){
//   return row.map(pixelRow => {
//     return pixelRow.forEach(pixel => {
//       return <div style={{width: '2px', height: '2px', backgroundColor: 'rgb(pixel)'}}></div>
//     })
//   })
// }

export function ScreenPreview() {
  const [screenData, setScreenData] = useState([]);

  useEffect(() => {
    getScreenData((event: MessageEvent<any>) => {
      setScreenData(JSON.parse(event.data));
    });
  }, []);

  return (
    <div>
      <table
        className="m-0"
        style={{ width: "200px", height: "200px" }}
        id="screen-preview"
      >
        {screenData.map((items: number[]) => {
          return (
            <tr className="">
              {items.map((pixels) => {
                return (
                  <td>
                    <div
                      style={{
                        width: "12px",
                        height: "12px",
                        backgroundColor: `rgb(${pixels})`,
                      }}
                    />
                  </td>
                );
              })}
            </tr>
          );
        })}
      </table>
    </div>
  );
}
