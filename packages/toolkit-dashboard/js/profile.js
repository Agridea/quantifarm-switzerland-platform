//binding:
//const bind_key = "qf-bind-key";
//qf-bind-key="userName"         > state["userName"]
//qf-bind-key="farms.farmName"   > state["farms"][state["farmsIndex"]]["farmName"]
//<select qf-bind-key="farmsIndex">      <option> �� ����� �� ������ "farms"

const state = {
    "userID": "1",
    "userName": "User Name 1",
    "userEmail": "a@server.com", 
    "userType": "Farmer", //Advisor, Policy Maker

    "farmsIndex": 0,
    "farms": [
        {
            "farmName": "Farm name 1",
            "farmCountry": "bg",
            "farmParcelArea": null,
        },
        {
            "farmName": "Farm name 2",
            "farmCountry": "de",
            "farmParcelArea": 10,
        },

    ],

    "otherData1": null,

}


console.log(state["userName"]);
console.log(state["farms"][state["farmsIndex"]]["farmName"]);



