import Hero from "@/components/home/hero";
import FeatureGrid from "@/components/home/feature-grid";
import CtaBanner from "@/components/home/cta-banner";

export default function Home() {
  return (
    <div className="flex flex-col gap-16 pb-10">
      {/* 1. Hero: Catch the judge's attention immediately */}
      <Hero />

      {/* 2. Features: Explain the 'How' and 'Why' */}
      <FeatureGrid />

      {/* 4. Final Call to Action */}
      <CtaBanner />
      
    </div>
  );
}