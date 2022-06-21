import { Card, Dropdown, Text } from "@nextui-org/react";

type CollectionElement<T> = any;
interface SetSlideProps {
  currentSlide: string | undefined,
  allSlides: string[] | undefined,
}
export function SetSlide({currentSlide, allSlides = []}: SetSlideProps) {

  const menuItems = allSlides.map(slide => {
    return {key: slide, slide}
  });

  return <div style={{ display: 'inline-block' }}>
    <Dropdown>
      <Dropdown.Trigger >
        <Card isHoverable isPressable css={{ maxWidth: '350px' }}>
          <Card.Body>
            <Text h2 className="text-center">{currentSlide ?? 'Loading...'}</Text>
          </Card.Body>
        </Card></Dropdown.Trigger>
        <Dropdown.Menu  items={menuItems}>
        {(item :CollectionElement<{key: string, slide: string}>) => (
          <Dropdown.Item
            key={item.key}
            color={item.key === "delete" ? "error" : "default"}
          >
            {item.slide}
          </Dropdown.Item>
        )}
      </Dropdown.Menu>
    </Dropdown>

  </div>

}