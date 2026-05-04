---
title: O pracovním portálu na junior.guru
template: main_about.html
---

{% from 'macros.html' import lead, note with context %}

# Vše o pracovním portálu

{% call lead() %}
Informace o [seznamu juniorních kandidátů](../candidates.jinja) a o [inzerátech pro juniory](../jobs.jinja). Záměr a hodnoty, se kterými je to provozováno. K tomu ještě pár zajímavých statistik.
{% endcall %}

[TOC]

## Historie inzerátů

Pracovní nabídky jsou na webu od jeho vzniku. Původně to měl být způsob, jak bude junior.guru vydělávat na svůj provoz, ale brzy se ukázalo, že to není dostatečně nosný zdroj příjmů. Inzerátů zadaných přímo přes junior.guru bylo jen pár, tak se časem zrodil systém, kdy se stahují nabídky z různých jiných portálů a pak třídí, aby zbyly jen ty vyloženě pro juniory.

Třídění bylo původně naprogramováno ručně a šlo zhruba o 20.000 řádků kódu. V roce 2024 systém přešel na analýzu pomocí AI. Stahování a třídění je náročné provozovat, ale juniorům je výsledek přístupný zdarma na webu.

Členové klubu mají inzeráty k dispozici v rámci Discordu, mohou tam o nich diskutovat a dovědět se okamžitě o přidávání nových.

## Historie seznamu kandidátů

Seznam kandidátů vznikl v roce 2025 jako reakce na otočku trhu, který začal být zdrženlivější a bylo stále těžší prosadit juniory do firem. Kandidáti se mohou do seznamu přidat zdarma, firmy mohou seznam zdarma používat. Pokud si kandidát platí za klub, tak je zvýrazněný.

Cílem je podpořit nábor juniorů ve firmách a odprezentovat juniory v tom nejlepším světle. Aby kandidáti měli určitou minimální laťku, je na seznam napojený systém denních kontrol. Pokud kandidát přestane laťku splňovat, spadne na konec seznamu a zobrazí se poloprůhledně.

Junioři si mohou z úvodní stránky junior.guru kdykoliv sami a zdarma spustit zpětnou vazbu na svůj profil, což by mělo sloužit jako zpětná vazba, jestli jsou už připraveni hledat si první práci.

## Počet inzerátů

Sloupcový graf ukazuje, kolik inzerátů bylo na portálu v jednotlivých týdnech. Barevně jsou rozděleny stažené a uveřejněné a zahozené inzeráty a inzeráty přidané na Discord ručně od členů klubu.

TODO

## Počet kandidátů

Sloupcový graf ukazuje, kolik kandidátů se na portálu prezentovalo v jednotlivých měsících. Barevně jsou rozděleni kandidáti z klubu, ostatní kandidáti, a kandidáti nesplňující „minimální laťku“.

TODO

## Počet zpětných vazeb na profily

Graf ukazuje počet zpětných vazeb na GitHub profily v jednotlivých měsících.

TODO
