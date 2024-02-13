import React from "react";
import styles from "./styles.module.scss";
import { ButtonLink } from "../common/Button";
import GreenText from "../common/GreenText";

const VerifRandBox = () => {
  return (
    <div className={styles.darkGreenBoxBis}>
      <div className="my-auto w-10/12 items-center">
        <h2 className="mb-4 text-lightGreen">Verifiable random function</h2>
        <GreenText isAligned={false} className="mb-10">
          Pragma offers a verifiable randomness feed that allows protocols to
          request secure randomness on-chain. The randomness proof is posted as
          calldata, and enables games, betting platforms or any other app to
          leverage verifiable randomness securely.
        </GreenText>
        <ButtonLink
          variant="outline"
          color="mint"
          href="https://docs.pragma.build/Resources/Cairo%201/randomness/randomness"
          center={false}
          className="w-fit"
        >
          Integrate VRF
        </ButtonLink>
      </div>
      <img
        className="items-center align-middle"
        src="/assets/vectors/verifRand.svg"
      />
    </div>
  );
};
export default VerifRandBox;
