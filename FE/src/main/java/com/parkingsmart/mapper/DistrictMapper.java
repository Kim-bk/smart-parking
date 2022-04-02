package com.parkingsmart.mapper;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.parkingsmart.dto.DistrictDTO;
import com.parkingsmart.entity.DistrictEntity;
import com.parkingsmart.service.impl.ProvinceService;

@Component
public class DistrictMapper {

	@Autowired
	private ModelMapper mapper;
	
	@Autowired
	private ProvinceService provinceService;
	
	@Autowired
	private ProvinceMapper provinceMapper;
	
	public DistrictDTO toDTO(DistrictEntity entity) {
		DistrictDTO dto = mapper.map(entity, DistrictDTO.class);
		dto.setIdProvince(entity.getProvince().getId());
		return dto;
	}
	
	public DistrictEntity toEntity(DistrictDTO dto) {
		DistrictEntity entity = mapper.map(dto, DistrictEntity.class);
		entity.setProvince(provinceMapper.ToEntity(provinceService.findOneById(dto.getIdProvince())));
		return entity;
	}
}
