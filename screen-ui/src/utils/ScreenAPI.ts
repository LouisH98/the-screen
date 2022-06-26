/*
An API that mirrors the REST API in the Python server
*/
import { ScreenStatus, rotations } from "./interfaces";

const HOSTNAME = "http://192.168.0.57:8000";

/**
 * Get the current status of The Screen
 * @returns Status of the screen, including current slide, brightness and more.
 */
export async function getStatus(): Promise<ScreenStatus> {
  return fetch(`${HOSTNAME}/status`, {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  }).then((res) => res.json());
}

/**
 * Returns the slides
 * @returns The list of slides current installed on the server
 * @throws Error
 */
export async function getSlides(): Promise<string[]> {
  return fetch(`${HOSTNAME}/slides`).then((res) => res.json());
}

/** 
Sets the brightness of the screen
@param brightness a value between 0 and 1 (1 being full brightness)
* @throws Error  
*/
export async function setBrightness(brightness: number): Promise<ScreenStatus> {
  return fetch(`${HOSTNAME}/brightness?value=${brightness}`, {
    method: "PUT",
  }).then((res) => res.json());
}

/** 
Sets the rotation of the screen
@param rotation rotation can be: 0, 90, 180, 270 degrees
* @throws Error  
*/
export async function setRotation(rotation: rotations): Promise<ScreenStatus> {
  return fetch(`${HOSTNAME}/rotations?value=${rotation}`, {
    method: "PUT",
  }).then((res) => res.json());
}

/**
 * Moves to the next slide
 * @returns The status of The Screen after changing slide
 * @throws Error
 */
export async function nextSlide(): Promise<ScreenStatus> {
  return fetch(`${HOSTNAME}/next-slide`).then((res) => res.json());
}

/**
 * Sets the slide to a specific one
 * @returns The status of The Screen after changing slide
 * @throws Error
 */
export async function setSlide(slideName: string): Promise<ScreenStatus> {
  const response: ScreenStatus | { status: string; message: string } =
    await fetch(`${HOSTNAME}/slide?slide_name=${slideName}`, {
      method: "PUT",
    }).then((res) => res.json());

  if ("status" in response && response["status"] === "ERROR") {
    throw new Error(response["message"]);
  }

  return response as ScreenStatus;
}

export async function getScreenData(
  callback: (event: MessageEvent<any>) => void
) {
  const eventSource = new EventSource(HOSTNAME + "/screen/stream");
  eventSource.addEventListener("screen_data", callback);
}
