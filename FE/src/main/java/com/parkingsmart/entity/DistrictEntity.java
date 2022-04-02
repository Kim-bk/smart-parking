package com.parkingsmart.entity;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;

@Entity(name="district")
public class DistrictEntity {
	
	@Id
	private String id;
	
	@Column
	private String name;
	
	@Column
	private String location;
	
	@Column
	private String type;
	
	@ManyToOne
	@JoinColumn(name="idProvince")
	private ProvinceEntity province;
	
	@OneToMany(mappedBy = "district")
	private List<WardEntity> wards = new ArrayList<WardEntity>();
	
	@OneToMany(mappedBy = "districtAddress")
	private List<AddressEntity> addresses = new ArrayList<AddressEntity>();


	public DistrictEntity() {
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

	public ProvinceEntity getProvince() {
		return province;
	}

	public void setProvince(ProvinceEntity province) {
		this.province = province;
	}

	public List<WardEntity> getWards() {
		return wards;
	}

	public void setWards(List<WardEntity> wards) {
		this.wards = wards;
	}

	public String getLocation() {
		return location;
	}

	public void setLocation(String location) {
		this.location = location;
	}

	public List<AddressEntity> getAddresses() {
		return addresses;
	}

	public void setAddresses(List<AddressEntity> addresses) {
		this.addresses = addresses;
	}


	
	
	

}
