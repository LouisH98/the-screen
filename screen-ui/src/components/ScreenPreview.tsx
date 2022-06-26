import { useEffect } from "react";
import { getScreenData } from "../utils/ScreenAPI";

export function ScreenPreview() {
  useEffect(() => {
    getScreenData((event: MessageEvent<any>) => {
      console.log(JSON.parse(event.data));
    });
  }, []);

  return <div>Here!</div>;
}
