import {
  Button,
  Dropdown,
  Text,
  NormalColors,
  StyledInputLabel,
} from "@nextui-org/react";
import { useState } from "react";
import { setSlide } from "../utils/ScreenAPI";

type CollectionElement<T> = any;

interface SetSlideProps {
  currentSlide: string | undefined;
  allSlides: string[] | undefined;
  getStatus: () => void;
}
export function SetSlide({
  currentSlide,
  allSlides = [],
  getStatus,
}: SetSlideProps) {
  const [buttonColour, setButtonColour] = useState("gradient");
  const [loading, setLoading] = useState(false);

  const menuItems = allSlides.map((slide) => {
    return { slide };
  });

  async function updateSlide(slideName: string) {
    try {
      setLoading(true);
      await setSlide(slideName);
      await getStatus();
      setButtonColour("success");
    } catch (e) {
      setButtonColour("error");
    } finally {
      setLoading(false);
      setTimeout(() => {
        setButtonColour("gradient");
      }, 500);
    }
  }

  return (
    <div style={{ display: "inline-block" }}>
      <StyledInputLabel>
        <Text small>Current Slide</Text>
      </StyledInputLabel>
      <Dropdown>
        <Dropdown.Trigger>
          <Button
            light={loading}
            shadow
            rounded
            auto
            disabled={loading}
            color={buttonColour as NormalColors}
            css={{ height: "70px", minWidth: "300px" }}
          >
            <Text h4 className="text-center">
              {currentSlide ?? "Loading..."}
            </Text>
          </Button>
        </Dropdown.Trigger>
        <Dropdown.Menu
          onAction={(key) => {
            updateSlide(key as string);
          }}
          color="primary"
          items={[...menuItems]}
        >
          {(item: CollectionElement<{ slide: string }>) => (
            <Dropdown.Item key={item.slide}>{item.slide}</Dropdown.Item>
          )}
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
}
