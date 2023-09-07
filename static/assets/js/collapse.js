const handicapRadio = document.querySelectorAll('input[name="handicap"]');
const handicapDescription = document.getElementById("handicapDescription");
const descriptionInput = document.getElementById("description");

handicapRadio.forEach((radio) => {
  radio.addEventListener("change", function () {
    if (this.value === "true") {
      handicapDescription.classList.remove("handicap_desc");
      descriptionInput.required = true;
    } else {
      handicapDescription.classList.add("handicap_desc");
      descriptionInput.required = false;
    }
  });
});
// phone number validator
document.addEventListener("DOMContentLoaded", function () {
  const phoneInputs = document.querySelectorAll(".phone input[type='tel']");
  const errorMessages = document.querySelectorAll(".phone .error-msg");

  phoneInputs.forEach(function (input, index) {
    input.addEventListener("input", function () {
      if (input.validity.patternMismatch) {
        errorMessages[index].textContent = "ከ 0 ውጭ ያሉትን ዘጠኝ አሃዞችን ያስገቡ";
        input.classList.add("error");
      } else {
        errorMessages[index].textContent = "";
        input.classList.remove("error");
      }
    });
  });
});
// service collapse
const inChurchRadio = document.querySelectorAll('input[name="inchurch"]');
const inChurchInput = document.getElementById("inChurch");
inChurchRadio.forEach((radio) => {
  radio.addEventListener("change", function () {
    const serviceRadio = document.querySelectorAll('input[name="service"]');
    const serviceInput = document.getElementById("serviceId");
    const serviceRadioChecked = document.getElementById("noService");
    if (this.value === "true") {
      inChurchInput.classList.remove("in_church");
      serviceRadio.forEach((radio) => {
        radio.addEventListener("change", function () {
          if (this.value == "true") {
            serviceInput.classList.remove("service_list");
          } else {
            serviceInput.classList.add("service_list");
          }
        });
      });
    } else {
      inChurchInput.classList.add("in_church");
      serviceInput.classList.add("service_list");
      serviceRadioChecked.checked = true;
    }
  });
});
// education status collapse
const eduCheckRadio = document.querySelectorAll('input[name="educheck"]');
const learnedInput = document.getElementById("learned");
const subOfStudyInput = document.getElementById("subOfStudy");
eduCheckRadio.forEach((radio) => {
  radio.addEventListener("change", function () {
    if (this.value === "true") {
      learnedInput.classList.remove("learned");
      subOfStudyInput.required = true;
    } else {
      learnedInput.classList.add("learned");
      subOfStudyInput.required = false;
    }
  });
});
// worlk status collapse
const iworkRadio = document.querySelectorAll('input[name="work_stats"]');
const iworkInput = document.getElementById("iWork");
const talentInput = document.getElementById("talent");
const professionInput = document.getElementById("profession");
const workPlaceInput = document.getElementById("workPlace");
const responibility = document.getElementById("responsiblity");
iworkRadio.forEach((radio) => {
  radio.addEventListener("change", function () {
    if (this.value === "true") {
      iworkInput.classList.remove("iwork");
      talentInput.required = true;
      professionInput.required = true;
      workPlaceInput.required = true;
      responibility.required = true;
    } else {
      iworkInput.classList.add("iwork");
      talentInput.required = false;
      professionInput.required = false;
      workPlaceInput.required = false;
      responibility.required = false;
    }
  });
});
// marrige status validator
const mStatusRadio = document.querySelectorAll('input[name="mstats"]');
const marriedForm = document.getElementById("maritalStatus");
const sFname = document.getElementById("sFName");
const sMname = document.getElementById("sMName");
const sLname = document.getElementById("sLName");
const dateOfWed = document.getElementById("dateOfWedding");

mStatusRadio.forEach((radio) => {
  radio.addEventListener("change", function () {
    const spauseInChurchRadio = document.querySelectorAll(
      'input[name="shere"]'
    );
    const ifHereOpt = document.getElementById("ifHere");
    if (this.value === "true") {
      marriedForm.classList.remove("maritial_bool");
      sFname.required = true;
      sMname.required = true;
      sLname.required = true;
      dateOfWed.required = true;
      spauseInChurchRadio.forEach((radio) => {
        radio.addEventListener("change", function () {
          const spouseInThisChurch =
            document.querySelectorAll('input[name="here"]');
          const notInThisChurchOpt = document.getElementById("noIfHere");
          const whereAreTheyInput = document.getElementById("whereAreThey");
          if (this.value === "true") {
            ifHereOpt.classList.remove("ifhere");
            spouseInThisChurch.forEach((radio) => {
              radio.addEventListener("change", function () {
                if (this.value === "false") {
                  notInThisChurchOpt.classList.remove("no_ifhere");
                  whereAreTheyInput.required = true;
                } else {
                  notInThisChurchOpt.classList.add("no_ifhere");
                  whereAreTheyInput.required = false;
                }
              });
            });
          } else {
            ifHereOpt.classList.add("ifhere");
          }
        });
      });
    } else {
      marriedForm.classList.add("maritial_bool");
      sFname.required = false;
      sMname.required = false;
      sLname.required = false;
      dateOfWed.required = false;
    }
  });
});

