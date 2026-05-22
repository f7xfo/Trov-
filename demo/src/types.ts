export interface Candidate {
  id: string;
  name: string;
  nameLatin: string;
  headline: LocaleString;
  location: LocaleString;
  salary: number;
  skills: string[];
  languages: string[];
  yearsExperience: number;
  ratingAvg: number;
  ratingCount: number;
  ratingCategories: RatingCategories;
  summary: LocaleString;
}

export interface RatingCategories {
  showedUpOnTime: number;
  skillsMatched: number;
  professionalConduct: number;
}

export interface LocaleString {
  km: string;
  en: string;
}

export interface SearchResult {
  query: string;
  candidates: Candidate[];
}
