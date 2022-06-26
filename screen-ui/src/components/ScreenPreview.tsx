import { useEffect } from "react";
import { getScreenData } from "../utils/ScreenAPI";

export function ScreenPreview() {
  useEffect(() => {
    getScreenData(console.log);
  }, []);

  return <div>Here!</div>;
}
