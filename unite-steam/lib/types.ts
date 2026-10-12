/** Reader pages with art pre-rendered on the server, so book data only reaches members. */
export type ReaderPage = {
  type: 'read' | 'choose';
  artSvg: string;
  kicker: string;
  line?: string;
  cue?: string;
  q?: string;
  note?: string;
  options?: { iconSvg: string; label: string; swapSvg: string | null }[];
  secs: number;
};

