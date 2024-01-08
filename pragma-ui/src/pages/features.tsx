import React from "react";
import { NextSeo } from "next-seo";
import Heading from "../components/Heading";
import { DefaultCTASection } from "../components/CTASection";
import FAQ from "../components/FAQ";
import FeaturesDisplay from "../components/Features/FeaturesDisplay";
import TimelineExplanation from "../components/TimelineExplanation";
import BoxContainer from "../components/common/BoxContainer";

const FeaturesPage = () => (
  <>
    <NextSeo title="Features" />
    <div className="w-full">
      <BoxContainer className="bg-dark">
        <Heading
          title="Reimagining Oracles"
          subtitle="Transparent, Decentralized &amp; Composable"
          text="Pragma Network has a uniquely robust and transparent architecture made possible by leveraging new zk-technology. "
          href="https://docs.pragmaoracle.com/docs/introduction"
          hrefText="Integrate verifiable data into your project"
        />
        <FeaturesDisplay />
      </BoxContainer>
      <BoxContainer className="bg-black">
        <Heading
          title="Step by Step Overview"
          subtitle="How it works"
          text="Follow along as the data moves from the sources on-chain and to your smart contract."
        />
        <TimelineExplanation />
      </BoxContainer>
      <BoxContainer className="bg-dark">
        <Heading
          title="Frequently asked questions"
          subtitle="Answers to"
          href="mailto:support@pragmaoracle.com?body=Hi%Pragma-Team,"
          hrefText="Send us your question"
        />
        <FAQ />
      </BoxContainer>
      <BoxContainer className="bg-black">
        <DefaultCTASection />
      </BoxContainer>
    </div>
  </>
);

export default FeaturesPage;
