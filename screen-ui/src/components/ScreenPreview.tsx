import { useEffect } from "react";

export function ScreenPreview() {
  useEffect(() => {
    const eventSource = new EventSource("/screen/stream");
    eventSource.addEventListener("screen_data", (event) => {
      console.log(event.data);
    });
  }, []);

  return <div>Here!</div>;
}
