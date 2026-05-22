import { useState } from 'react';
import type { Candidate, SearchResult } from './types';

// ── Mock Data ──

const MOCK_CANDIDATES: Candidate[] = [
  {
    id: "1",
    name: "សុខ ម៉ាលី",
    nameLatin: "Sok Maly",
    headline: { km: "ចុងភៅ បទពិសោធន៍ ៥ ឆ្នាំ សៀមរាប", en: "Cook, 5 years experience, Siem Reap" },
    location: { km: "សៀមរាប", en: "Siem Reap" },
    salary: 350,
    skills: ["Khmer cooking", "Thai cooking", "POS systems"],
    languages: ["Khmer", "English (basic)"],
    yearsExperience: 5,
    ratingAvg: 4.8,
    ratingCount: 12,
    ratingCategories: {
      showedUpOnTime: 0.92,
      skillsMatched: 0.88,
      professionalConduct: 0.95,
    },
    summary: {
      km: "ចុងភៅជំនាញខ្មែរ និងថៃ មានបទពិសោធន៍ ៥ ឆ្នាំនៅសៀមរាប។ ធ្លាប់ធ្វើការនៅភោជនីយដ្ឋានធំៗ។",
      en: "Skilled Khmer and Thai cook with 5 years of experience in Siem Reap. Worked at established restaurants."
    }
  },
  {
    id: "2",
    name: "ជា ដារ៉ា",
    nameLatin: "Chea Dara",
    headline: { km: "អ្នកបើកឡាន បទពិសោធន៍ ៣ ឆ្នាំ ភ្នំពេញ", en: "Driver, 3 years experience, Phnom Penh" },
    location: { km: "ភ្នំពេញ", en: "Phnom Penh" },
    salary: 400,
    skills: ["Driving license B", "Motorbike", "English speaking"],
    languages: ["Khmer", "English"],
    yearsExperience: 3,
    ratingAvg: 4.2,
    ratingCount: 5,
    ratingCategories: {
      showedUpOnTime: 0.80,
      skillsMatched: 0.85,
      professionalConduct: 0.90,
    },
    summary: {
      km: "អ្នកបើកឡានដែលអាចទុកចិត្តបាន ស្គាល់ផ្លូវភ្នំពេញច្បាស់។ អតីតអ្នកបើកឡានក្រុមហ៊ុន។",
      en: "Reliable driver with excellent knowledge of Phnom Penh. Former company driver."
    }
  },
  {
    id: "3",
    name: "គឹម ស្រីនាង",
    nameLatin: "Kim Sreyneang",
    headline: { km: "បុគ្គលិកលក់ ភ្នំពេញ ចេះភាសាចិន", en: "Sales Staff, Phnom Penh, Chinese-speaking" },
    location: { km: "ភ្នំពេញ", en: "Phnom Penh" },
    salary: 300,
    skills: ["Sales", "Inventory", "POS", "Customer service"],
    languages: ["Khmer", "Chinese", "English (basic)"],
    yearsExperience: 2,
    ratingAvg: 4.5,
    ratingCount: 8,
    ratingCategories: {
      showedUpOnTime: 0.95,
      skillsMatched: 0.82,
      professionalConduct: 0.90,
    },
    summary: {
      km: "បុគ្គលិកលក់ដែលមានភាពរួសរាយរាក់ទាក់ មានបទពិសោធន៍នៅហាងលក់ទំនិញ។ ចេះភាសាចិន។",
      en: "Friendly sales associate with retail experience. Chinese-speaking — ideal for shops with Chinese clientele."
    }
  },
  {
    id: "4",
    name: "វង្ស សុភាព",
    nameLatin: "Vong Sopheap",
    headline: { km: "សន្តិសុខ ភ្នំពេញ ៤ ឆ្នាំ", en: "Security Guard, Phnom Penh, 4 years" },
    location: { km: "ភ្នំពេញ", en: "Phnom Penh" },
    salary: 280,
    skills: ["Security", "CCTV monitoring", "First aid"],
    languages: ["Khmer"],
    yearsExperience: 4,
    ratingAvg: 3.9,
    ratingCount: 3,
    ratingCategories: {
      showedUpOnTime: 0.90,
      skillsMatched: 0.75,
      professionalConduct: 0.85,
    },
    summary: {
      km: "សន្តិសុខមានបទពិសោធន៍ ធ្លាប់ធ្វើការនៅធនាគារ។ មានវិញ្ញាបនបត្រសង្រ្គោះបឋម។",
      en: "Experienced security guard, previously at a bank. First-aid certified."
    }
  },
  {
    id: "5",
    name: "ផល រិទ្ធី",
    nameLatin: "Phal Rithy",
    headline: { km: "អ្នករត់តុ សៀមរាប ចេះអង់គ្លេស", en: "Waiter, Siem Reap, English-speaking" },
    location: { km: "សៀមរាប", en: "Siem Reap" },
    salary: 250,
    skills: ["Service", "English", "Barista"],
    languages: ["Khmer", "English"],
    yearsExperience: 2,
    ratingAvg: 0,
    ratingCount: 0,
    ratingCategories: { showedUpOnTime: 0, skillsMatched: 0, professionalConduct: 0 },
    summary: {
      km: "អ្នករត់តុដែលមានថាមពល និងមានបទពិសោធន៍នៅភោជនីយដ្ឋានសៀមរាប។ ចេះធ្វើកាហ្វេ។",
      en: "Energetic waiter with experience in Siem Reap restaurants. Can make coffee."
    }
  },
];

// ── Types ──

type Lang = 'km' | 'en';
type Page = 'home' | 'profile';

// ── Translations ──

const t = (key: string, lang: Lang): string => {
  const dict: Record<string, Record<Lang, string>> = {
    tagline: { km: "ស្វែងរកបុគ្គលិក — ឥតគិតថ្លៃ បើកចំហ គួរឱ្យទុកចិត្ត", en: "Find workers — free, open, trustworthy" },
    searchPlaceholder: { km: "ឧ. អ្នកធ្វើម្ហូបនៅសៀមរាប ក្រោម $400", en: 'e.g. "cook in Siem Reap under $400"' },
    searchBtn: { km: "ស្វែងរក", en: "Search" },
    resultsTitle: { km: "លទ្ធផល", en: "Results" },
    resultsFound: { km: "រកឃើញ {count} បេក្ខជន", en: "Found {count} candidates" },
    noResults: { km: "មិនទាន់មានបេក្ខជនត្រូវគ្នាទេ", en: "No matching candidates yet" },
    back: { km: "← ត្រឡប់ទៅលទ្ធផល", en: "← Back to results" },
    yearsExp: { km: "ឆ្នាំ", en: "yrs" },
    salaryUnit: { km: "/ខែ", en: "/mo" },
    contact: { km: "📩 ទាក់ទង", en: "📩 Contact" },
    reportProfile: { km: "រាយការណ៍ប្រវត្តិរូបនេះ", en: "Report this profile" },
    about: { km: "អំពី", en: "About" },
    skills: { km: "ជំនាញ", en: "Skills" },
    languages: { km: "ភាសា", en: "Languages" },
    location: { km: "ទីតាំង", en: "Location" },
    experience: { km: "បទពិសោធន៍", en: "Experience" },
    salary: { km: "ប្រាក់ខែ", en: "Salary" },
    ratingHistory: { km: "ប្រវត្តិវាយតម្លៃ", en: "Rating History" },
    showedUp: { km: "មកទាន់ពេល", en: "Showed up on time" },
    skillsMatch: { km: "ជំនាញត្រូវគ្នា", en: "Skills matched profile" },
    professional: { km: "ឥរិយាបថវិជ្ជាជីវៈ", en: "Professional conduct" },
    newUnrated: { km: "ថ្មី — មិនទាន់មានការវាយតម្លៃ", en: "New — not yet rated" },
    welcomeTitle: { km: "ស្វាគមន៍មកកាន់ Trov 🇰🇭", en: "Welcome to Trov 🇰🇭" },
    welcomeText: { km: "វេទិកាជ្រើសរើសបុគ្គលិកបើកចំហ ឥតគិតថ្លៃសម្រាប់កម្ពុជា។ សាកល្បងស្វែងរកខាងក្រោម៖", en: "Open-source, free recruitment for Cambodia. Try a search below:" },
    footer: { km: "Trov · បើកចំហ · ឥតគិតថ្លៃ · គ្មានការលក់ទិន្នន័យ · MIT License", en: "Trov · Open Source · Free Forever · No Data Selling · MIT License" },
  };
  return dict[key]?.[lang] ?? key;
};

// ── Components ──

function RatingBadge({ avg, count, lang }: { avg: number; count: number; lang: Lang }) {
  if (count === 0) {
    return <span className="rating-badge" style={{ color: 'var(--text-muted)' }}>{t('newUnrated', lang)}</span>;
  }
  return (
    <span className="rating-badge">
      <span className="rating-star">⭐</span> {avg.toFixed(1)}
      <span className="rating-count">({count})</span>
    </span>
  );
}

function CandidateCard({ candidate, lang, onClick }: { candidate: Candidate; lang: Lang; onClick: () => void }) {
  return (
    <div className="candidate-card" onClick={onClick}>
      <div className="card-header">
        <div>
          <div className="card-name">{candidate.name}</div>
          <div className="card-headline">{candidate.headline[lang]}</div>
        </div>
        <RatingBadge avg={candidate.ratingAvg} count={candidate.ratingCount} lang={lang} />
      </div>
      <div className="card-meta">
        <span className="card-meta-item">📍 {candidate.location[lang]}</span>
        <span className="card-meta-item">💼 {candidate.yearsExperience}{t('yearsExp', lang)}</span>
        <span className="card-meta-item">💰 ${candidate.salary}{t('salaryUnit', lang)}</span>
      </div>
      <div className="card-skills">
        {candidate.skills.slice(0, 3).map(s => <span key={s} className="skill-tag">{s}</span>)}
        {candidate.skills.length > 3 && <span className="skill-tag">+{candidate.skills.length - 3}</span>}
      </div>
    </div>
  );
}

function CandidateProfile({ candidate, lang, onBack }: { candidate: Candidate; lang: Lang; onBack: () => void }) {
  return (
    <div className="container">
      <button className="profile-back" onClick={onBack}>{t('back', lang)}</button>

      <div className="profile-header">
        <div className="profile-name">{candidate.name}</div>
        <div className="profile-headline">{candidate.headline[lang]}</div>
        <div className="profile-rating-row">
          <span className="profile-rating-big">
            {candidate.ratingCount > 0 ? `⭐ ${candidate.ratingAvg.toFixed(1)}` : '—'}
          </span>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
            {candidate.ratingCount > 0 ? `${candidate.ratingCount} ratings` : t('newUnrated', lang)}
          </span>
        </div>
      </div>

      {candidate.ratingCount > 0 && (
        <div className="profile-section">
          <div className="profile-section-title">{t('ratingHistory', lang)}</div>
          <div className="rating-categories">
            <div className="rating-category">
              <span className="rating-category-label">{t('showedUp', lang)}</span>
              <span className="rating-category-value pct">{Math.round(candidate.ratingCategories.showedUpOnTime * 100)}%</span>
            </div>
            <div className="rating-category">
              <span className="rating-category-label">{t('skillsMatch', lang)}</span>
              <span className="rating-category-value pct">{Math.round(candidate.ratingCategories.skillsMatched * 100)}%</span>
            </div>
            <div className="rating-category">
              <span className="rating-category-label">{t('professional', lang)}</span>
              <span className="rating-category-value pct">{Math.round(candidate.ratingCategories.professionalConduct * 100)}%</span>
            </div>
          </div>
        </div>
      )}

      <div className="profile-section">
        <div className="profile-section-title">{t('about', lang)}</div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', lineHeight: 1.6 }}>{candidate.summary[lang]}</p>
      </div>

      <div className="profile-section">
        <div className="profile-section-title">Details</div>
        <div className="profile-meta-grid">
          <div className="profile-meta-item">
            <div className="profile-meta-label">{t('location', lang)}</div>
            <div className="profile-meta-value">{candidate.location[lang]}</div>
          </div>
          <div className="profile-meta-item">
            <div className="profile-meta-label">{t('experience', lang)}</div>
            <div className="profile-meta-value">{candidate.yearsExperience} {t('yearsExp', lang)}</div>
          </div>
          <div className="profile-meta-item">
            <div className="profile-meta-label">{t('salary', lang)}</div>
            <div className="profile-meta-value">${candidate.salary}{t('salaryUnit', lang)}</div>
          </div>
          <div className="profile-meta-item">
            <div className="profile-meta-label">{t('languages', lang)}</div>
            <div className="profile-meta-value">{candidate.languages.join(', ')}</div>
          </div>
        </div>
      </div>

      <div className="profile-section">
        <div className="profile-section-title">{t('skills', lang)}</div>
        <div className="card-skills">
          {candidate.skills.map(s => <span key={s} className="skill-tag">{s}</span>)}
        </div>
      </div>

      <button className="contact-btn">{t('contact', lang)}</button>
      <div className="report-link">{t('reportProfile', lang)}</div>
    </div>
  );
}

function HomePage({ lang, onSelect }: { lang: Lang; onSelect: (c: Candidate) => void }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult | null>(null);
  const [searching, setSearching] = useState(false);

  const handleSearch = () => {
    if (!query.trim()) return;
    setSearching(true);
    setTimeout(() => {
      const q = query.toLowerCase();
      const matches = MOCK_CANDIDATES.filter(c =>
        c.skills.some(s => s.toLowerCase().includes(q)) ||
        c.headline.en.toLowerCase().includes(q) ||
        c.headline.km.includes(query) ||
        c.location.en.toLowerCase().includes(q) ||
        c.name.toLowerCase().includes(q)
      );
      setResults({ query, candidates: matches });
      setSearching(false);
    }, 800);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSearch();
  };

  const handleTeaser = (q: string) => {
    setQuery(q);
    // trigger search
    setTimeout(() => {
      const matches = MOCK_CANDIDATES.filter(c =>
        c.skills.some(s => s.toLowerCase().includes(q)) ||
        c.headline.en.toLowerCase().includes(q) ||
        c.location.en.toLowerCase().includes(q)
      );
      setResults({ query: q, candidates: matches });
    }, 500);
  };

  return (
    <>
      <div className="search-section">
        <div className="search-tagline">{t('tagline', lang)}</div>
        <div className="search-bar">
          <input
            className="search-input"
            placeholder={t('searchPlaceholder', lang)}
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button className="search-btn" onClick={handleSearch} disabled={searching}>
            {searching ? '...' : t('searchBtn', lang)}
          </button>
        </div>
      </div>

      {results ? (
        <div className="results-section">
          <div className="results-header">
            <span className="results-count">
              {t('resultsFound', lang).replace('{count}', String(results.candidates.length))}
            </span>
            {results.query && <span> · "{results.query}"</span>}
          </div>
          {results.candidates.length === 0 ? (
            <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '24px' }}>
              {t('noResults', lang)}
            </p>
          ) : (
            results.candidates.map(c => (
              <CandidateCard key={c.id} candidate={c} lang={lang} onClick={() => onSelect(c)} />
            ))
          )}
        </div>
      ) : (
        <div className="welcome-section">
          <div className="welcome-emoji">🇰🇭</div>
          <div className="welcome-title">{t('welcomeTitle', lang)}</div>
          <div className="welcome-text">{t('welcomeText', lang)}</div>
          <div className="teaser-queries">
            {[
              { km: "អ្នកធ្វើម្ហូបនៅសៀមរាប", en: "cook siem reap" },
              { km: "អ្នកបើកឡាននៅភ្នំពេញ", en: "driver phnom penh" },
              { km: "បុគ្គលិកលក់ ចេះចិន", en: "sales chinese speaking" },
            ].map(q => (
              <button key={q[lang]} className="teaser-query" onClick={() => handleTeaser(q.en)}>
                🔍 {lang === 'km' ? q.km : q.en}
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

// ── App ──

export default function App() {
  const [lang, setLang] = useState<Lang>('km');
  const [page, setPage] = useState<Page>('home');
  const [selected, setSelected] = useState<Candidate | null>(null);

  const handleSelect = (candidate: Candidate) => {
    setSelected(candidate);
    setPage('profile');
  };

  const handleBack = () => {
    setPage('home');
  };

  return (
    <div className={lang === 'km' ? 'lang-km' : ''}>
      <header className="header">
        <div className="header-logo">
          TROV<span>.work</span>
        </div>
        <div style={{ display: 'flex', gap: 4 }}>
          <button
            className={`lang-toggle ${lang === 'km' ? 'active' : ''}`}
            onClick={() => setLang('km')}
          >
            ភាសាខ្មែរ
          </button>
          <button
            className={`lang-toggle ${lang === 'en' ? 'active' : ''}`}
            onClick={() => setLang('en')}
          >
            English
          </button>
        </div>
      </header>

      {page === 'home' && <HomePage lang={lang} onSelect={handleSelect} />}
      {page === 'profile' && selected && <CandidateProfile candidate={selected} lang={lang} onBack={handleBack} />}

      <footer className="footer">
        <p>{t('footer', lang)}</p>
      </footer>
    </div>
  );
}
