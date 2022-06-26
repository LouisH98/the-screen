import { Card } from "@nextui-org/react";
import { useEffect, useRef, useState } from "react";
import { getScreenData } from "../utils/ScreenAPI";

export function ScreenPreview() {
  const [screenData, setScreenData] = useState([]);
  const [isListening, setIsListening] = useState(true);
  let stopEvents = useRef(() => {});

  function startListening() {
    const stopReceivingEvents = getScreenData((event: MessageEvent<any>) => {
      setScreenData(JSON.parse(event.data));
    });
    setIsListening(true);
    stopEvents.current = stopReceivingEvents;
  }

  function stopListening() {
    stopEvents.current();
    setIsListening(false);
  }

  useEffect(() => {
    startListening();

    return () => {
      stopListening();
    };
  }, []);

  return (
    <div
      style={{ display: "flex" }}
      className="m-2 justify-center items-center"
    >
      <Card
        onPress={() => (isListening ? stopListening() : startListening())}
        variant="shadow"
        isHoverable
        isPressable
        css={{ width: "226px" }}
      >
        <table
          className="m-0 p-5"
          style={{
            width: "200px",
            height: "200px",
            backgroundColor: "black",
            filter: isListening ? "grayscale(0)" : "grayscale(1)",
            transition: "filter 0.5s",
          }}
          id="screen-preview"
        >
          <tbody>
            {screenData.map((items: number[], index) => {
              return (
                <tr key={index}>
                  {items.map((pixels, iIndex) => {
                    return (
                      <td key={iIndex}>
                        <div
                          style={{
                            width: "12px",
                            height: "12px",
                            borderRadius: "100%",
                            backgroundColor: `rgb(${pixels})`,
                          }}
                        />
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
