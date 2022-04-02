package com.parkingsmart.entity;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.OneToMany;

@Entity(name="province")
public class ProvinceEntity {

	@Id
	private String id;
	
	@Column
	private String name;
	
	@Column
	private String type;
	
	@OneToMany(mappedBy = "province")
	private List<DistrictEntity> districts = new ArrayList<DistrictEntity>();
	
	@OneToMany(mappedBy = "provinceAddress")
	private List<AddressEntity> addresses = new ArrayList<AddressEntity>();

	public ProvinceEntity() {
		super();
	}

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}
	
	
}
