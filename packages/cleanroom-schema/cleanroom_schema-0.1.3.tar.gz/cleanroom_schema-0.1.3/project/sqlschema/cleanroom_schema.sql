

CREATE TABLE "Agent" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "AnalyticalSample" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "DataListCollection" (
	biosample_list TEXT, 
	frs_list TEXT, 
	cbfs_list TEXT, 
	nt_list TEXT, 
	PRIMARY KEY (biosample_list, frs_list, cbfs_list, nt_list)
);

CREATE TABLE "FieldResearchSite" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "MaterialEntity" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "NamedThing" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE "Biosample" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	collected_from TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(collected_from) REFERENCES "FieldResearchSite" (id)
);

CREATE TABLE "CollectingBiosamplesFromSite" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	participating_agent TEXT, 
	has_outputs TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(participating_agent) REFERENCES "Agent" (id)
);

CREATE TABLE "PlannedProcess" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	has_inputs TEXT, 
	has_outputs TEXT, 
	participating_agent TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(participating_agent) REFERENCES "Agent" (id)
);

CREATE TABLE "Site" (
	id TEXT NOT NULL, 
	name TEXT, 
	description TEXT, 
	"CollectingBiosamplesFromSite_id" TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY("CollectingBiosamplesFromSite_id") REFERENCES "CollectingBiosamplesFromSite" (id)
);
